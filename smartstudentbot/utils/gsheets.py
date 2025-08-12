import gspread_asyncio
from google.oauth2.service_account import Credentials
from typing import Optional, List, Dict, Any

from ..config import GOOGLE_CREDS, SHEET_ID, USERS_SHEET_NAME
from .logger import logger

class GSheetsManager:
    """
    Manages all interactions with Google Sheets.
    Handles authentication and provides async CRUD operations.
    """
    def __init__(self, creds: Optional[dict], sheet_id: Optional[str]):
        self.creds = creds
        self.sheet_id = sheet_id
        self.agcm: Optional[gspread_asyncio.AsyncioGspreadClientManager] = None
        self.spreadsheet: Optional[gspread_asyncio.AsyncioGspreadSpreadsheet] = None

    def get_creds(self):
        """Prepares credentials for gspread."""
        if not self.creds:
            return None
        # Scopes needed for Sheets and Drive
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        return Credentials.from_service_account_info(self.creds, scopes=scopes)

    async def initialize(self):
        """Initializes the connection to the Google Spreadsheet."""
        if not self.creds or not self.sheet_id:
            logger.warning("Google Sheets credentials or Sheet ID not provided. GSheetsManager disabled.")
            return

        try:
            self.agcm = gspread_asyncio.AsyncioGspreadClientManager(self.get_creds)
            agc = await self.agcm.authorize()
            self.spreadsheet = await agc.open_by_key(self.sheet_id)
            logger.info(f"Successfully connected to Google Sheet: '{await self.spreadsheet.get_title()}'")
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets connection: {e}")
            self.spreadsheet = None

    async def _get_worksheet(self, sheet_name: str) -> Optional[gspread_asyncio.AsyncioGspreadWorksheet]:
        """Helper to get a worksheet by name, creating it if it doesn't exist."""
        if not self.spreadsheet:
            return None
        try:
            return await self.spreadsheet.worksheet(sheet_name)
        except gspread_asyncio.gspread.exceptions.WorksheetNotFound:
            logger.warning(f"Worksheet '{sheet_name}' not found. Attempting to create it.")
            try:
                return await self.spreadsheet.add_worksheet(title=sheet_name, rows=100, cols=20)
            except Exception as e:
                logger.error(f"Failed to create worksheet '{sheet_name}': {e}")
                return None
        except Exception as e:
            logger.error(f"Error accessing worksheet '{sheet_name}': {e}")
            return None

    async def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Finds a user profile by their Telegram ID."""
        ws = await self._get_worksheet(USERS_SHEET_NAME)
        if not ws:
            return None
        try:
            # Assumes 'telegram_id' is in the first column
            cell = await ws.find(str(user_id), in_column=1)
            if cell:
                headers = await ws.row_values(1)
                values = await ws.row_values(cell.row)
                return dict(zip(headers, values))
            return None
        except gspread_asyncio.gspread.exceptions.CellNotFound:
            return None
        except Exception as e:
            logger.error(f"Error fetching user {user_id}: {e}")
            return None

    async def save_user_profile(self, user_data: Dict[str, Any]):
        """Saves or updates a user profile."""
        ws = await self._get_worksheet(USERS_SHEET_NAME)
        if not ws:
            logger.error("Cannot save user profile, worksheet not available.")
            return

        try:
            headers = await ws.row_values(1)
            if not headers:
                headers = list(user_data.keys())
                await ws.append_row(headers, value_input_option='USER_ENTERED')

            # Check if user exists to update, otherwise append
            user_id_str = str(user_data.get('telegram_id'))
            cell = await ws.find(user_id_str, in_column=1)

            row_data = [str(user_data.get(h, '')) for h in headers]

            if cell:
                # Update existing user
                await ws.update(f'A{cell.row}', [row_data], value_input_option='USER_ENTERED')
                logger.info(f"Updated profile for user {user_id_str} in row {cell.row}")
            else:
                # Add new user
                await ws.append_row(row_data, value_input_option='USER_ENTERED')
                logger.info(f"Appended new profile for user {user_id_str}")

        except Exception as e:
            logger.error(f"Failed to save user profile for {user_data.get('telegram_id')}: {e}")

    async def append_row_to_sheet(self, sheet_name: str, data: List[Any]):
        """Appends a single row to the specified sheet."""
        ws = await self._get_worksheet(sheet_name)
        if not ws:
            logger.error(f"Cannot append row, worksheet '{sheet_name}' not available.")
            return
        try:
            await ws.append_row(data, value_input_option='USER_ENTERED')
            logger.info(f"Appended row to '{sheet_name}'.")
        except Exception as e:
            logger.error(f"Failed to append row to '{sheet_name}': {e}")


# Global instance
gsheets_manager = GSheetsManager(GOOGLE_CREDS, SHEET_ID)
