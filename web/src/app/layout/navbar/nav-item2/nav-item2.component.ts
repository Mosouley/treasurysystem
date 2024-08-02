import { Component } from '@angular/core';
import { MenuNode } from '../menu-node';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-nav-item2',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './nav-item2.component.html',
  styleUrl: './nav-item2.component.css'
})
export class NavItem2Component {
  links: MenuNode[] = [
    {
      name: 'User',
      url: 'home/login',
      icon: 'speed',
      action: false,
      expandable: true,
      children: [
        {
          name: 'Login',
          url: 'home/login',
          icon: 'category',
          action: false,
          expandable: true
        },
        {
          name: 'Register',
          url: 'profile',
          icon: 'category',
          action: false,
          expandable: true,
        }
      ]
    },
    {
      name: 'Office',
      url: 'login',
      icon: 'speed',
      action: false,
      expandable: true,}
    ]

}
