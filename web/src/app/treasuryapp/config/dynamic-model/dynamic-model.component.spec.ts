import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DynamicModelComponent } from './dynamic-model.component';

describe('DynamicModelComponent', () => {
  let component: DynamicModelComponent;
  let fixture: ComponentFixture<DynamicModelComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DynamicModelComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DynamicModelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
