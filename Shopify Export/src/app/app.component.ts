import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { InventoryRemovalComponent } from './inventory-removal/inventory-removal.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, InventoryRemovalComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'shopify-export-app';
}
