import { Component } from '@angular/core';
import { InventoryService } from '../services/inventory.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CSC } from '../models/csc.models';
import * as XLSX from 'xlsx';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {
  // --- Input State ---
  sku: string = '';
  location: string = '';
  targetServiceRate: number = 98;
  
  // We'll let users type "10, 12, 15..." instead of asking 10 separate times
  leadTimeInput: string = ''; 
  
  csvData: any[] = [];
  parsedFileName: string = '';

  // --- Output State ---
  forecast: CSC | null = null;
  errorMessage: string = '';

  forecastHistory: { sku: string, location: string, data: CSC }[] = [];

  constructor(private inventoryService: InventoryService) {}

  // 1. Handle File Upload (Replaces excel.py loading)
  onFileUpload(event: any) {
    this.errorMessage = '';
    const target: DataTransfer = <DataTransfer>(event.target);
    
    if (target.files.length !== 1) {
      this.errorMessage = 'Cannot use multiple files';
      return;
    }

    const file = target.files[0];
    this.parsedFileName = file.name;

    const reader: FileReader = new FileReader();

    reader.onload = (e: any) => {
      try {
        const arrayBuffer = e.target.result;
        const workbook: XLSX.WorkBook = XLSX.read(arrayBuffer, { type: 'array' });
        
        // Find latest year sheet
        const sheetNames = workbook.SheetNames;
        let targetSheetName = sheetNames[0];

        // 1. Map through sheets and attempt to extract a 4-digit year
        const sheetsWithYears = sheetNames
          .map(name => {
            // Regex to find any 4-digit sequence (e.g., '2025' inside 'Year 2025 Final')
            const match = name.match(/\d{4}/); 
            return {
              originalName: name,
              year: match ? parseInt(match[0], 10) : null
            };
          })
          .filter(sheet => sheet.year !== null) // 2. Throw out sheets with no year
          .sort((a, b) => b.year! - a.year!);   // 3. Sort descending (highest year first)

        // 4. Pick the winner or use the fallback
        if (sheetsWithYears.length > 0) {
          targetSheetName = sheetsWithYears[0].originalName;
          console.log(`Extracted year ${sheetsWithYears[0].year} from sheet "${targetSheetName}"`);
        } else {
          targetSheetName = sheetNames[sheetNames.length - 1]; 
          console.log(`No years found. Falling back to last sheet: "${targetSheetName}"`);
        }

        const worksheet: XLSX.WorkSheet = workbook.Sheets[targetSheetName];
        
        // FIX: Load the sheet as a 2D Array of strings, instead of objects. 
        // This bypasses the multi-line header issue completely.
        const rawData: any[][] = XLSX.utils.sheet_to_json(worksheet, { header: 1, defval: "" });
        
        if (rawData.length === 0) throw new Error("File is empty.");

        // Utility: Scans the first 10 rows to find which column index holds a keyword
        const findColIdx = (keywords: string[]) => {
          for (let r = 0; r < Math.min(10, rawData.length); r++) {
            if (!rawData[r]) continue;
            for (let c = 0; c < rawData[r].length; c++) {
              const cellVal = String(rawData[r][c]).trim().toLowerCase();
              for (const kw of keywords) {
                if (cellVal === kw || (kw.length > 2 && cellVal.includes(kw))) {
                  return c; // We found the column number!
                }
              }
            }
          }
          return -1; // Keyword not found
        };

        // 1. Locate the exact column number for every required field
        const skuIdx = findColIdx(['sku', 'item', 'item sku']);
        const locIdx = findColIdx(['location', 'loc', 'warehouse']);
        const srvIdx = findColIdx(['srv', 'service', 'van']);

        const months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'];
        const monthIndices: { [key: string]: number } = {};
        months.forEach(m => {
          monthIndices[m] = findColIdx([m, m + '.', m + 'uary', m + 'ruary', m + 'ch', m + 'il', m + 'e', m + 'y', m + 'ust', m + 'ember', m + 'ober']);
        });

        if (skuIdx === -1) {
          this.errorMessage = 'Could not find a column named "SKU" or "Item" in the top 5 rows.';
          return;
        }

        // 2. Loop through the raw data and build clean objects
        const cleanedData: any[] = [];
        
        for (let i = 0; i < rawData.length; i++) {
          const row = rawData[i];
          if (!row || row.length === 0) continue;

          // Extract the SKU string to check if this is an actual data row
          const cellSku = skuIdx < row.length ? String(row[skuIdx]).trim() : '';
          
          // Skip empty rows and rows that are clearly just the header labels
          if (!cellSku || cellSku.toLowerCase() === 'sku' || cellSku.toLowerCase() === 'item') {
             continue;
          }

          // Build a perfectly formatted object for our DataProcessor
          const obj: any = {};
          obj['sku'] = cellSku;
          if (locIdx !== -1 && locIdx < row.length) obj['location'] = row[locIdx];
          if (srvIdx !== -1 && srvIdx < row.length) obj['srv'] = row[srvIdx];
          
          months.forEach(m => {
            const idx = monthIndices[m];
            obj[m] = (idx !== -1 && idx < row.length) ? row[idx] : 0; 
          });
          
          cleanedData.push(obj);
        }

        this.csvData = cleanedData;
        console.log(`Successfully mapped Data:`, this.csvData);

      } catch (error: any) {
        this.errorMessage = 'Error parsing Excel file: ' + error.message;
        console.error(error);
      }
    };

    reader.readAsArrayBuffer(file);
  }

  // 2. Run Calculations (Replaces the main execution loop)
  calculate() {
    this.forecastHistory = [];
    this.errorMessage = '';
    this.forecast = null;

    // Convert comma-separated string "10, 12, 14" into number array [10, 12, 14]
    const freshLeadTimesArray = this.leadTimeInput
      .split(',')
      .map(val => Number(val.trim()))
      .filter(val => !isNaN(val));

    if (freshLeadTimesArray.length === 0) {
      this.errorMessage = 'Please enter at least one valid lead time.';
      return;
    }

    if (!this.csvData.length) {
      this.errorMessage = 'Please upload a xlsx file first.';
      return;
    }

    if (this.sku.trim().toUpperCase() === 'ALL') {
      this.processAllSkus(freshLeadTimesArray);
      return; // Stop here so it doesn't run the single-SKU logic below
    }

    // Call the Service
    const result = this.inventoryService.generateForecast(
      this.csvData,
      this.sku,
      this.location,
      freshLeadTimesArray,
      this.targetServiceRate
    );

    if (result) {
      this.forecast = result;

      const isDuplicate = this.forecastHistory.some(item => item.sku === this.sku && item.location === this.location);
      if (!isDuplicate) {
        this.forecastHistory.push({ sku: this.sku, location: this.location, data: result });
      }
    } else {
      this.errorMessage = `Could not find SKU "${this.sku}" at Location "${this.location}"`;
    }
  }

  processAllSkus(leadTimes: number[]) {
    // 1. Gather all headers to dynamically find the SKU and Location columns
    const allHeaders = new Set<string>();
    this.csvData.forEach(row => Object.keys(row).forEach(key => allHeaders.add(key)));
    const headerRow: any = {};
    allHeaders.forEach(key => headerRow[key] = '');

    // 2. Identify the keys (using the same logic as your DataProcessor)
    const skuKey = this.findKey(headerRow, ['sku', 'item', 'item sku']);
    const locKey = this.findKey(headerRow, ['location', 'loc', 'warehouse']);

    if (!skuKey) {
      this.errorMessage = 'Could not identify the SKU column in the uploaded file.';
      return;
    }

    // 3. Extract unique SKU + Location pairs
    const uniqueItems = new Map<string, { sku: string, loc: string }>();
    this.csvData.forEach(row => {
      const rowSku = row[skuKey] ? String(row[skuKey]).trim() : '';
      const rowLoc = (locKey && row[locKey]) ? String(row[locKey]).trim() : '';
      
      if (rowSku) {
        const uniqueKey = `${rowSku}_${rowLoc}`; // Combine them to ensure uniqueness
        if (!uniqueItems.has(uniqueKey)) {
          uniqueItems.set(uniqueKey, { sku: rowSku, loc: rowLoc });
        }
      }
    });

    // 4. Run the calculation for every unique item
    let successCount = 0;
    uniqueItems.forEach(item => {
      const result = this.inventoryService.generateForecast(
        this.csvData, item.sku, item.loc, leadTimes, this.targetServiceRate
      );

      if (result) {
        // Prevent adding exact duplicates to the history table
        const isDuplicate = this.forecastHistory.some(
          historyItem => historyItem.sku === item.sku && historyItem.location === item.loc
        );
        if (!isDuplicate) {
          this.forecastHistory.push({ sku: item.sku, location: item.loc, data: result });
        }
        successCount++;
      }
    });

    // 5. Update the UI
    this.forecast = null; // Clear the single-item view to focus on the history box
    this.errorMessage = `Successfully processed ${successCount} SKUs. Scroll down to export them to Excel.`;
  }

  // Helper function to find column names regardless of capitalization
  private findKey(row: any, keywords: string[]): string | null {
    const keys = Object.keys(row);
    for (const keyword of keywords) {
      for (const key of keys) {
        const cleanKey = key.trim().toLowerCase();
        if (cleanKey === keyword || (keyword.length > 2 && cleanKey.includes(keyword))) {
          return key;
        }
      }
    }
    return null;
  }

  exportToExcel() {
    if (this.forecastHistory.length === 0) return;

    console.log("EXCEL EXPORT TRIGGERED. Current History Array:", this.forecastHistory);

    // 1. Map our history array into the exact columns you requested
    const exportData = this.forecastHistory.map(item => {
      
      // Format the lead time dictionary into a clean string (e.g., "30 Days: 5, 45 Days: 8")
      const leadTimeDict = item.data.getReorderQuantityNumDays();
      const leadTimeStr = Object.entries(leadTimeDict)
        .map(([days, qty]) => `${days} Days: ${qty}`)
        .join(' | ');

      return {
        'SKU': item.sku,
        'Location': item.location,
        'Total Sales': item.data.getTotal(),
        'Average Monthly Sales': item.data.getMeanRounded(),
        'Average Daily Sales': item.data.getMeanDailyRounded(),
        'Safety Stock Quantity': item.data.getSafetyStockWithLeadTimeRounded(),
        'Reorder Point': item.data.getReorderPointWithLeadTime(),
        'Annual Reorder Quantity': item.data.getReorderQuantity(),
        'Reorder Quantities (Lead Time Days)': leadTimeStr
      };
    });

    // 2. Convert the mapped data to an Excel worksheet
    const worksheet: XLSX.WorkSheet = XLSX.utils.json_to_sheet(exportData);
    
    // 3. Create a new workbook and append the worksheet
    const workbook: XLSX.WorkBook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Forecasts');

    // 4. Save the file to the user's computer
    XLSX.writeFile(workbook, 'Inventory_Forecast_Multiple.xlsx');
  }
}
