import { Component, ComponentFactoryResolver, ElementRef, HostListener, OnInit, Type } from '@angular/core';
import { trigger, state, style, animate, transition } from '@angular/animations';

import { CommonModule } from '@angular/common';
import { MaterialModule } from '../../material/material.module';
import { BannerService } from '../../shared/services/banner.service';


@Component({
  selector: 'app-banner',
  templateUrl: './banner.component.html',
  styleUrls: ['./banner.component.css'],
  standalone: true,
  imports: [
    CommonModule,
    MaterialModule,

  ],
  animations: [
    trigger('slideInOut', [
      state('true', style({
        right: '0',
      })),
      state('false', style({
        right: '-100%',
      })),
      transition('true => false', animate('300ms ease-in-out')),
      transition('false => true', animate('300ms ease-in-out')),
    ]),
  ],
})
export class BannerComponent implements OnInit{
  public bannerState = false;
  dynamicComponentType: Type<any> | null = null;


  constructor(private bannerService: BannerService,
    private componentFactoryResolver: ComponentFactoryResolver,
     private elementRef: ElementRef){}

  ngOnInit(){
    this.bannerService.bannerState$.subscribe((state) => {
      this.bannerState = state;
    });

    this.bannerService.getDynamicComponent().subscribe((componentType) => {
      this.dynamicComponentType = componentType;
    });
  }

  @HostListener('document:click', ['$event'])
  handleClickOutside(event: Event) {
    if (this.bannerState ==true && !this.elementRef.nativeElement.contains(event.target)) {

    }
  }

  toggleBanner(){
    this.bannerService.toggleBanner()
  }

}
