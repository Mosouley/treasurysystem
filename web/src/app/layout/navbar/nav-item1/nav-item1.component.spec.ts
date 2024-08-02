import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NavItem1Component } from './nav-item1.component';

describe('NavItem1Component', () => {
  let component: NavItem1Component;
  let fixture: ComponentFixture<NavItem1Component>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NavItem1Component]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NavItem1Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
