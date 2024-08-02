import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WalletsizingComponent } from './walletsizing.component';

describe('WalletsizingComponent', () => {
  let component: WalletsizingComponent;
  let fixture: ComponentFixture<WalletsizingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
    imports: [WalletsizingComponent]
})
    .compileComponents();

    fixture = TestBed.createComponent(WalletsizingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
