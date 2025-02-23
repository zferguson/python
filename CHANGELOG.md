# 📝 CHANGELOG

This file documents changes made to the repository, including new features, improvements, and bug fixes. Follow the semantic versioning format (`MAJOR.MINOR.PATCH`).

---

## 📌 Versioning Format:
- **MAJOR** (X.0.0) – Breaking changes or significant updates
- **MINOR** (0.X.0) – New features added, but backward-compatible
- **PATCH** (0.0.X) – Bug fixes, performance improvements, or small changes

---

## **[Unreleased]**
### 🆕 New Features
- Placeholder for upcoming features.

### 🔧 Fixes & Improvements
- Placeholder for upcoming fixes.

---

## **[1.2.0] - YYYY-MM-DD**
### 🆕 New Features
- Added automated testing for data integrity (`tests/test_data_integrity.py`).
- Introduced a configuration file (`config.yaml`) for dashboard parameters.

### 🔧 Fixes & Improvements
- Optimized SQL queries in `client_dashboard.sql` for better performance.
- Updated documentation in `data_governance_policy.md`.

---

## **[1.1.3] - YYYY-MM-DD**
### 🛠️ Bug Fixes
- Fixed incorrect date parsing in `extract_data.py`.
- Resolved permissions issue with database connection in `db_connection.py`.

---

## **[1.1.0] - YYYY-MM-DD**
### 🆕 New Features
- Added `CODEOWNERS` file to enforce review approvals.
- Introduced `CONTRIBUTING.md` to standardize contributions.

### 🔧 Fixes & Improvements
- Refactored ETL scripts to improve modularity.

---

## **[1.0.0] - YYYY-MM-DD**
### 🎉 Initial Release
- Set up repository structure for dashboards, ad-hoc requests, and scripts.
- Implemented first version of `sales_dashboard.ipynb` and `client_dashboard.sql`.

---

### 📜 How to Update the Changelog
1. **Before merging a PR**, update `CHANGELOG.md` under the `[Unreleased]` section.
2. Once a new version is released, move items from `[Unreleased]` into a dated version section.
3. Follow the format:
   ```markdown
   ## [X.Y.Z] - YYYY-MM-DD
   - Short description of change.