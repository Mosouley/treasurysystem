import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MaterialModule } from '../../material/material.module';
import { childRoutes } from '../child-routes';




@Component({
  selector: 'app-side-nav-closed',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MaterialModule],
  templateUrl: './side-nav-closed.component.html',
  styleUrl: './side-nav-closed.component.css'
})
export class SideNavClosedComponent implements OnInit {
    routes = childRoutes;
    constructor() { }

    ngOnInit(): void {
    }
}
