import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NavItem2Component } from './nav-item2.component';

describe('NavItem2Component', () => {
  let component: NavItem2Component;
  let fixture: ComponentFixture<NavItem2Component>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NavItem2Component]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NavItem2Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
