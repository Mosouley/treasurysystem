import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PnlSummaryComponent } from './pnl-summary.component';

describe('PnlSummaryComponent', () => {
  let component: PnlSummaryComponent;
  let fixture: ComponentFixture<PnlSummaryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PnlSummaryComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PnlSummaryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
