import aiohttp
import asyncio
import pandas as pd
import logging
import time
import asyncpg
from aiolimiter import AsyncLimiter
from typing import List, Dict, Any, Optional

# Configure logging
logging.basicConfig(
    filename="async_api_data.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class CyberArkClient:
    """
    Fetches security credentials securely from CyberArk.
    """

    def __init__(self, cyberark_url: str, app_id: str, safe: str, object_name: str):
        self.cyberark_url = cyberark_url
        self.app_id = app_id
        self.safe = safe
        self.object_name = object_name

    async def fetch_credentials(self) -> Optional[Dict[str, str]]:
        """
        Fetches credentials from CyberArk's REST API.

        Returns:
            dict: Retrieved credentials (e.g., API key, DB password).
        """
        url = f"{self.cyberark_url}/AIMWebService/api/Accounts"
        params = {
            "AppID": self.app_id,
            "Safe": self.safe,
            "Object": self.object_name
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data  # Typically contains {"UserName": ..., "Content": ...}
                    else:
                        logging.error(f"Failed to retrieve credentials: {response.status}")
                        return None
            except Exception as e:
                logging.error(f"CyberArk request failed: {e}")
                return None


class AsyncAPIDataFetcher:
    """
    Fetches API data asynchronously with CyberArk authentication, retry logic, and PostgreSQL storage.
    """

    def __init__(self, base_url: str, endpoint: str, cyberark_client: CyberArkClient, 
                 max_retries: int = 3, timeout: int = 10, rate_limit: int = 10, db_url: Optional[str] = None):
        self.base_url = base_url
        self.endpoint = endpoint
        self.max_retries = max_retries
        self.timeout = timeout
        self.rate_limiter = AsyncLimiter(rate_limit, 1)  # Max X requests per second
        self.db_url = db_url
        self.cyberark_client = cyberark_client
        self.api_key = None  # Will be retrieved from CyberArk

    async def fetch_credentials(self):
        """
        Retrieves the API key securely from CyberArk before making API requests.
        """
        credentials = await self.cyberark_client.fetch_credentials()
        if credentials and "Content" in credentials:
            self.api_key = credentials["Content"]
            logging.info("Successfully retrieved API key from CyberArk.")
        else:
            logging.error("Failed to retrieve API key from CyberArk.")

    async def fetch(self, session: aiohttp.ClientSession, url: str, retry_count: int = 0) -> Optional[Dict[str, Any]]:
        """
        Fetches a single API response with retries and rate limiting.
        """
        async with self.rate_limiter:  # Apply rate limiting
            try:
                headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}

                async with session.get(url, headers=headers, timeout=self.timeout) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logging.warning(f"Request failed ({response.status}): {url}")
                        return None

            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                logging.error(f"Request error: {e}. Retry {retry_count + 1}/{self.max_retries}")

                if retry_count < self.max_retries:
                    await asyncio.sleep(2 ** retry_count)  # Exponential backoff
                    return await self.fetch(session, url, retry_count + 1)

        return None

    async def fetch_all(self, urls: List[str]) -> List[Dict[str, Any]]:
        """
        Fetches multiple API responses asynchronously.
        """
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(session, url) for url in urls]
            responses = await asyncio.gather(*tasks)
            return [res for res in responses if res]  # Remove failed requests

    async def save_to_postgres(self, df: pd.DataFrame):
        """
        Saves the DataFrame to PostgreSQL.
        """
        if not self.db_url:
            logging.warning("No database URL provided, skipping PostgreSQL storage.")
            return
        
        try:
            conn = await asyncpg.connect(self.db_url)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS api_data (
                    id SERIAL PRIMARY KEY,
                    name TEXT,
                    value FLOAT
                )
            """)

            values = [(row["id"], row["name"], row["value"]) for _, row in df.iterrows()]
            await conn.executemany("INSERT INTO api_data (id, name, value) VALUES ($1, $2, $3)", values)

            await conn.close()
            logging.info(f"Stored {len(df)} records in PostgreSQL.")
        except Exception as e:
            logging.error(f"Database error: {e}")

    def save_to_parquet(self, df: pd.DataFrame, filename: str = "output.parquet"):
        """
        Saves the DataFrame to a Parquet file.
        """
        df.to_parquet(filename, engine="pyarrow", index=False)
        logging.info(f"Data saved to {filename}")

    def run(self, urls: List[str]):
        """
        Orchestrates fetching, validation, and storage of API data.
        """
        asyncio.run(self.fetch_credentials())  # Get API Key securely

        if not self.api_key:
            logging.error("API key retrieval failed, aborting data fetch.")
            return None

        start_time = time.time()
        responses = asyncio.run(self.fetch_all(urls))
        end_time = time.time()

        if not responses:
            logging.error("No data retrieved.")
            return None

        df = pd.DataFrame(responses)
        asyncio.run(self.save_to_postgres(df))  # Store in PostgreSQL
        self.save_to_parquet(df)  # Save to Parquet

        logging.info(f"Fetched {len(df)} records in {end_time - start_time:.2f} seconds.")
        return df

# Example usage
if __name__ == "__main__":
    # CyberArk Configuration
    cyberark_url = "https://cyberark.example.com"
    app_id = "my-app-id"
    safe = "API_Credentials_Safe"
    object_name = "MyAPIKey"

    # API Configuration
    base_url = "https://jsonplaceholder.typicode.com"
    endpoint = "posts"
    db_url = "postgresql://user:password@localhost:5432/mydatabase"

    urls = [f"{base_url}/{endpoint}/{i}" for i in range(1, 101)]
    cyberark_client = CyberArkClient(cyberark_url, app_id, safe, object_name)

    fetcher = AsyncAPIDataFetcher(base_url, endpoint, cyberark_client, rate_limit=10, db_url=db_url)
    df = fetcher.run(urls)

    if df is not None:
        print("Data successfully fetched, stored, and saved.")
        print(df.head())
    else:
        print("Data retrieval failed.")