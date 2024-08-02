import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RisksMetricsComponent } from './risks-metrics.component';

describe('RisksMetricsComponent', () => {
  let component: RisksMetricsComponent;
  let fixture: ComponentFixture<RisksMetricsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RisksMetricsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RisksMetricsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
