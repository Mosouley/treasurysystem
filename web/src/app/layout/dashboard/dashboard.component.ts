import { CommonModule, NgOptimizedImage } from '@angular/common';
import { MaterialModule } from './../../material/material.module';
import { Component, OnInit } from '@angular/core';
import { Card } from '../../model/daily_rate';
import { ChartComponent } from '../../report/chart/chart.component';
import { StatComponent } from '../../treasuryapp/stat/stat.component';


@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [StatComponent,
    MaterialModule,
     CommonModule,
    ChartComponent,
    NgOptimizedImage
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit {

  cards: Array<Card> = [];
  orders_count = 10;
  reviews_count = 150;
  clicks_count = 430;
  shares_count = 43;

  ngOnInit() {
    this.cards = [
      {
        imgSrc: 'assets/img/peoplew.jpg',
        name: 'Understanding',
        description: `In-depth knowledge and experience make it possible to solve problems. Thanks TheDigitalArtist for the image(pixabay.com thedigitalartist-202249)`
      },
      {
        imgSrc: 'assets/img/59.jpg',
        name: 'Planing',
        description: `Plan before doing anything. That will help to make a quality product. Thanks lukasbieri for the image(pixabay.com lukasbieri-4664461)`
      },
      {
        imgSrc: 'assets/img/teamw.jpg',
        name: 'Implementing',
        description: `Implement quickly what we have planed. Do revisions until you satisfy. Thanks geralt for the image(pixabay.com geralt-9301)`
      }
    ];
  }
}
