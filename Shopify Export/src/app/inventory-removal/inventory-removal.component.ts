import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ShopifyInventoryService, LocationRemovalPayload } from '../shopify-inventory.service';
import { environment } from '../../environment/environment';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-inventory-removal',
  templateUrl: './inventory-removal.component.html',
  styleUrls: ['./inventory-removal.component.css'],
  imports: [CommonModule],
  standalone: true
})
export class InventoryRemovalComponent {
  selectedFile: File | null = null;
  parsedData: LocationRemovalPayload[] = [];
  
  // UI States
  isParsing = false;
  isUploading = false;
  successMessage = '';
  errorMessage = '';

  // This will be the URL of your Python backend later
  private readonly BACKEND_API_URL = `${environment.apiUrl}/remove-locations`;

  constructor(
    private inventoryService: ShopifyInventoryService,
    private http: HttpClient
  ) {}

  /**
   * Captures the file when the user selects it via the input.
   */
  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
      this.resetMessages();
      this.processFile();
    }
  }

  /**
   * Passes the file to our service for Papa Parse to handle.
   */
  private processFile(): void {
    if (!this.selectedFile) return;
    
    this.isParsing = true;
    this.inventoryService.parseInventoryCsv(this.selectedFile).subscribe({
      next: (data) => {
        this.parsedData = data;
        this.isParsing = false;
      },
      error: (err) => {
        this.errorMessage = `Error parsing file: ${err}`;
        this.isParsing = false;
      }
    });
  }

  /**
   * Sends the clean, extracted array to the Python backend.
   */
  syncWithShopify(): void {
    if (this.parsedData.length === 0) {
      this.errorMessage = 'No valid "not stocked" items found to sync.';
      return;
    }

    this.isUploading = true;
    this.resetMessages();

    this.http.post(this.BACKEND_API_URL, { items: this.parsedData }).subscribe({
      next: (response: any) => {
        this.successMessage = `Successfully processed ${this.parsedData.length} items.`;
        this.isUploading = false;
        this.parsedData = []; 
      },
      error: (err) => {
        this.errorMessage = 'Failed to sync with the server. Check your backend connection.';
        this.isUploading = false;
      }
    });
  }

  private resetMessages(): void {
    this.successMessage = '';
    this.errorMessage = '';
  }
}

