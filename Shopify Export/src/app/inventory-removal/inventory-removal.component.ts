import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ShopifyInventoryService, LocationRemovalPayload } from '../shopify-inventory.service';
import { environment } from '../../environment/environment';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-inventory-removal',
  templateUrl: './inventory-removal.component.html',
  styleUrls: ['./inventory-removal.component.css'],
  imports: [CommonModule, FormsModule],
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

  storeUrl = '';
  accessToken = '';
  apiVersion = '2024-01'; 

  isTesting = false;
  testSuccessMessage = '';
  testErrorMessage = '';

  private readonly TEST_API_URL = 'http://localhost:5000/api/test-connection';
  
  private readonly BACKEND_API_URL = `${environment.apiUrl}/remove-locations`;

  constructor(
    private inventoryService: ShopifyInventoryService,
    private http: HttpClient
  ) {}

  testConnection(): void {
    if (!this.storeUrl || !this.accessToken) {
      this.testErrorMessage = 'Please enter your Store URL and Access Token first.';
      return;
    }

    this.isTesting = true;
    this.testSuccessMessage = '';
    this.testErrorMessage = '';

    const payload = {
      storeUrl: this.storeUrl,
      accessToken: this.accessToken,
      apiVersion: this.apiVersion
    };

    this.http.post(this.TEST_API_URL, payload).subscribe({
      next: (response: any) => {
        this.testSuccessMessage = response.message;
        this.isTesting = false;
      },
      error: (err) => {
        // We look for our custom error message from Python, or fall back to a generic one
        this.testErrorMessage = err.error?.error || 'Failed to connect to the server.';
        this.isTesting = false;
      }
    });
  }

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
      this.resetMessages();
      this.processFile();
    }
  }

  syncWithShopify(): void {
    // Basic validation to ensure they filled out the fields
    if (!this.storeUrl || !this.accessToken) {
      this.errorMessage = 'Please provide your Shopify Store URL and Access Token.';
      return;
    }

    if (this.parsedData.length === 0) {
      this.errorMessage = 'No valid "not stocked" items found to sync.';
      return;
    }

    this.isUploading = true;
    this.resetMessages();

    // Package the credentials AND the items into one payload
    const payload = {
      credentials: {
        storeUrl: this.storeUrl.replace('https://', '').trim(),
        accessToken: this.accessToken.trim(),
        apiVersion: this.apiVersion.trim()
      },
      items: this.parsedData
    };

    this.http.post(this.BACKEND_API_URL, payload).subscribe({
      next: (response: any) => {
        this.successMessage = `Successfully processed ${this.parsedData.length} items.`;
        this.isUploading = false;
        this.parsedData = []; // Clear out data after success
      },
      error: (err) => {
        this.errorMessage = 'Failed to sync with the server. Check your backend connection.';
        this.isUploading = false;
      }
    });
  }

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

  private resetMessages(): void {
    this.successMessage = '';
    this.errorMessage = '';
  }
}
