import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FxflowsComponent } from './fxflows.component';

describe('FxflowsComponent', () => {
  let component: FxflowsComponent;
  let fixture: ComponentFixture<FxflowsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
    imports: [FxflowsComponent]
})
    .compileComponents();

    fixture = TestBed.createComponent(FxflowsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
