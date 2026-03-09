import { TestBed } from '@angular/core/testing';

import { ShopifyInventoryService } from './shopify-inventory.service';

describe('ShopifyInventoryService', () => {
  let service: ShopifyInventoryService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ShopifyInventoryService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
