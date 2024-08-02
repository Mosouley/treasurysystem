import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PositionCcyComponent } from './position-ccy.component';

describe('PositionCcyComponent', () => {
  let component: PositionCcyComponent;
  let fixture: ComponentFixture<PositionCcyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PositionCcyComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PositionCcyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
