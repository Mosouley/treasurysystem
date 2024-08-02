import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { MenuNode } from '../menu-node';

@Component({
  selector: 'app-nav-login',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './nav-login.component.html',
  styleUrl: './nav-login.component.css'
})
export class NavLoginComponent {
  
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

    ]
}
