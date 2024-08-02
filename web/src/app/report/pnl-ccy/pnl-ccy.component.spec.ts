import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PnlCcyComponent } from './pnl-ccy.component';

describe('PnlCcyComponent', () => {
  let component: PnlCcyComponent;
  let fixture: ComponentFixture<PnlCcyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PnlCcyComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PnlCcyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
