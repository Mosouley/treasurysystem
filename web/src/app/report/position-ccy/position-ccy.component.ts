import { MaterialModule } from './../../material/material.module';
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CurrenciesService } from '../../shared/services/currencies.service';
import { PositionsService } from '../../shared/services/positions.service';
import { ReportComponent } from '../report-template/report.component';
import { DataModel } from '../../model/data.model';

@Component({
  selector: 'app-position-ccy',
  standalone: true,
  imports: [ReportComponent, CommonModule, MaterialModule],
  templateUrl: './position-ccy.component.html',
  styleUrl: './position-ccy.component.css'
})
export class PositionCcyComponent implements OnInit {
  currencies: any[] = []
  reportingData!: any[]  ;
  model: DataModel[] = [];
  reportName = 'Position'
  today = new Date()
  constructor(private ccyService: CurrenciesService,
    private positionServ: PositionsService
  ) {}

  ngOnInit(): void {
    this.loadAllCurrencies()
    // this.model = [
    //   new DataModel('ccy', 'Currencies', 'string', false,  'uppercase'),
    //   new DataModel('position.', 'Op. Position', 'number', false,  '`number:`1.2-2`'),
    //   new DataModel('position', 'Intraday', 'number', false, [], '`number:`1.2-2`'),]
    this.linkedHeaders()
    this.fetchPositions()
  }

  loadAllCurrencies(): void {
    this.loadCurrenciesPage();
    this.reportingData = [...this.currencies]
    this.fetchPositions()
  }

  loadCurrenciesPage(next?: string): void {

    this.ccyService.listByUrl(next).subscribe(data => {
      this.currencies = [...this.currencies, ...data.results];
         if (this.currencies.length < data.count) {
          this.loadCurrenciesPage(data.next);
         }

    });


  }
  fetchPositions(){
    this.positionServ.listByUrl().subscribe(data => {
      this.reportingData =  data.filter((model: any) => {
        const txDate = new Date(model['date']);
        // console.log(model['']);
        
        return (
          txDate.setHours(0, 0, 0, 0) >= this.today.setHours(0, 0, 0, 0) &&
          txDate.setHours(0, 0, 0, 0) <= this.today.setHours(0, 0, 0, 0)
        );
      });

    })
    console.log(this.reportingData );
    this.reportingData.forEach(model => {
      console.log(model['ccy__code']);
      
    })
    
  }

  linkedHeaders(){
    this.model = this.currencies.map(ccy => {
      console.log(ccy);

      return new DataModel(ccy.code, ccy.code, 'number', false, [], '`number:`1.2-2`')
    })

  }
}
