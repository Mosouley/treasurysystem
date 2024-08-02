import { formatDate } from '@angular/common';
import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MaterialModule } from '../../material/material.module';
import { DataModel } from '../../model/data.model';
import { FilterComponent } from '../../report/filter/filter.component';
import { ReportComponent } from '../../report/report-template/report.component';
import { TradeService } from '../../shared/services/trade.service';


@Component({
  selector: 'app-sales-by-period',
  standalone: true,
  imports: [MaterialModule,
              ReportComponent,
              FilterComponent],
  templateUrl: './sales-by-period.component.html',
  styleUrl: './sales-by-period.component.css',
})
export class SalesByPeriodComponent implements OnInit {
  @ViewChild(FilterComponent) filterComponent!: FilterComponent;

  reportingData!: any[];
  model: DataModel[] = [];
  start = new Date();
  end = new Date();
  reportName = 'FX Blotter from ';
  filteredData: any[] = [];
  isLoading = false;


  constructor(
    private route: ActivatedRoute,
    private tradeServ: TradeService
  ) {}
  ngOnInit(): void {
    this.model = [
      new DataModel(
        'customer',
        'Customer',
        'Array',
        false,
        'name',
        'uppercase'
      ),
      new DataModel('product', 'Product', 'Array', false, 'name', 'uppercase'),
      new DataModel('id', 'TradeId', 'string', false, [], 'uppercase'),
      new DataModel('val_date', 'ValDate', 'date', false, [], 'date:shortDate'),
      new DataModel('tx_date', 'TxDate', 'date', false, [], 'date:shortDate'),
      new DataModel('ccy1', 'Ccy1', 'Array', false, 'code', 'uppercase'),
      new DataModel('ccy2', 'Ccy2', 'Array', false, 'code', 'uppercase'),
      new DataModel('buy_sell', 'Buy/Sell', 'string', false, []),
      new DataModel('amount1','Ccy1_Amount','number', true,[],'`number:`1.2-2`'
      ),
      new DataModel(
        'amount2',
        'Ccy2_Amount',
        'number',
        false,
        [],
        '`number:`1.2-2`'
      ),
      new DataModel(
        'deal_rate',
        'DealRate',
        'number',
        false,
        [],
        '`number:`1.2-2`'
      ),
      new DataModel(
        'system_rate',
        'ReevalRate',
        'number',
        false,
        [],
        '`number:`1.2-2`'
      ),
      new DataModel(
        'fees_rate',
        'Other Fees',
        'number',
        false,
        [],
        '`number:`1.2-2`'
      ),
      new DataModel('deal_pnl', 'PnL000', 'number', false, []),
      new DataModel('trader', 'Dealer', 'Array', false, 'name', 'uppercase'),
      new DataModel('status', 'Status', 'string', false, [], 'uppercase'),
      new DataModel(
        'last_updated',
        'Last. Up',
        'time',
        false,
        [],
        'date:`h:mm a`'
      ),
    ];
    this.reportingData = this.route.snapshot.data['trades']?.results;
    this.setPeriod();
    this.fetchingData()
  }

  onReportingPeriodChange(newValue: any): void {
    // Handle changes to yourVariable in real-time
    this.start = newValue.timePeriod.startDay;
    this.end = newValue.timePeriod.endDay;
    this.setPeriod();
  }

  fetchData(start: Date, end: Date) {

    this.isLoading = true
    const start_date = start.toISOString().split('T')[0]
    const end_date = end.toISOString().split('T')[0]


   this.tradeServ.fetchData({ start_date,end_date}).subscribe(data => {

    this.reportingData = data.results
    this.isLoading = false
   })
    // this.filterData(start, end);
    //  let myHeaders = new Headers();
    // myHeaders.append("apikey", "PVZKPPNf2FmqHagUcU0JJVG5NIEDuxY0");

    // let requestOptions = {
    //   method: 'GET',
    //   redirect: 'follow',
    //   headers: myHeaders
    // };

  }
  filterData(start: Date, end: Date) {

    this.filteredData = this.reportingData?.filter((model: any) => {
      const txDate = new Date(model['tx_date']);
      return (
        txDate.setHours(0, 0, 0, 0) >= start.setHours(0, 0, 0, 0) &&
        txDate.setHours(0, 0, 0, 0) <= end.setHours(0, 0, 0, 0)
      );
    });
   

  }
  setPeriod() {
    this.reportName = '';

    this.reportName =
      'FX Blotter  from ' +
      `${formatDate(this.start.toString(), 'mediumDate', 'en-US')}` +
      ' To ' +
      `${formatDate(this.end.toString(), 'mediumDate', 'en-US')}`;
    // this.filterData(this.start, this.end);
    // refetch the data


    this.fetchData(this.start, this.end)
  }

fetchingData() {
//     let myHeaders = new Headers();
// myHeaders.append("apikey", "PVZKPPNf2FmqHagUcU0JJVG5NIEDuxY0");

// const start_date = "2024-01-01";
// const end_date = "2024-05-19";
// const base_ccy ='USD'

// try {
//   const response = await fetch(`https://api.apilayer.com/exchangerates_data/timeseries?start_date=${start_date}&end_date=${end_date}&base=${base_ccy}`, {
//     method: 'GET',
//     redirect: 'follow',
//     headers: myHeaders
//   });

//   console.log(response);

//   if (!response.ok) {
//     throw new Error(`HTTP error! status: ${response.status}`);
//   }

//    const result:any = await response.text();
//   console.log(result['rates']);
// } catch (error) {
//   console.log('error', error);
// }
  }
}
