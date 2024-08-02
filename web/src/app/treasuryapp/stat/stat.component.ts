import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MaterialModule } from '../../material/material.module';


@Component({
  selector: 'app-stat',
  standalone: true,
  imports: [ CommonModule, MaterialModule],
  templateUrl: './stat.component.html',
  styleUrl: './stat.component.css'
})
export class StatComponent {
  @Input() icon!: string;
  @Input() count!: number;
  @Input() label!: string;
}
