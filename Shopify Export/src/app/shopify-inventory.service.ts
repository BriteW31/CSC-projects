import { Injectable } from '@angular/core';
import * as Papa from 'papaparse';
import { Observable, Observer } from 'rxjs';

// Define the structure we want to send to the Python backend
export interface LocationRemovalPayload {
  inventoryItemId: string;
  locationId: string;
}

@Injectable({
  providedIn: 'root'
})
export class ShopifyInventoryService {

  constructor() { }

  /**
   * Parses the uploaded CSV file and extracts the items marked for removal.
   */
  public parseInventoryCsv(file: File): Observable<LocationRemovalPayload[]> {
    return new Observable((observer: Observer<LocationRemovalPayload[]>) => {
      
      Papa.parse(file, {
        header: true,         // Reads the first row as keys
        skipEmptyLines: true, // Ignores trailing empty lines
        complete: (result) => {
          try {
            const extractedData = this.extractRemovalData(result.data);
            observer.next(extractedData);
            observer.complete();
          } catch (error) {
            observer.error('Failed to process CSV data formatting.');
          }
        },
        error: (error) => {
          observer.error(error.message);
        }
      });
    });
  }

  /**
   * Filters and maps the raw CSV data into our clean Payload interface.
   */
  private extractRemovalData(rawData: any[]): LocationRemovalPayload[] {
    const payload: LocationRemovalPayload[] = [];

    rawData.forEach(row => {
      // NOTE: You will need to adjust these bracket notations to match 
      // the EXACT column headers in your specific Excel/CSV export.
      const inventoryItemId = row['Inventory Item ID'];
      const locationId = row['Location ID'];
      const quantity = row['Quantity']; // Or whatever column you typed "not stocked" into

      // Only grab the rows where you specifically typed "not stocked"
      if (quantity && quantity.toString().trim().toLowerCase() === 'not stocked') {
        if (inventoryItemId && locationId) {
          payload.push({
            inventoryItemId: inventoryItemId.toString().trim(),
            locationId: locationId.toString().trim()
          });
        }
      }
    });

    return payload;
  }
}
