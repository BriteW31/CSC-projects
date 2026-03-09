import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InventoryRemovalComponent } from './inventory-removal.component';

describe('InventoryRemovalComponent', () => {
  let component: InventoryRemovalComponent;
  let fixture: ComponentFixture<InventoryRemovalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InventoryRemovalComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(InventoryRemovalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
