import { WebsocketService } from './../../shared/services/websocket.service';
import { ChangeDetectionStrategy, Component, signal, Inject, Injectable, OnDestroy, OnInit, inject } from '@angular/core';
import { TradeFormComponent } from './trade-form.component';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';

import { formatDate } from '@angular/common';
import { ReportComponent } from '../../report/report-template/report.component';
import { DataModel } from '../../model/data.model';
import { API_URLS } from '../../shared/config/app.url.config';
import { ReportContainerComponent } from '../../report/report-container/report-container.component';
import { MatExpansionModule } from '@angular/material/expansion';

@Component({
    selector: 'app-tradesflow',
    templateUrl: './tradesflow.component.html',
    styleUrls: ['./tradesflow.component.css'],
    standalone: true,
    imports: [ReportComponent, 
      ReportContainerComponent,
      MatExpansionModule],
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class TradesflowComponent implements OnInit,OnDestroy {

  reportingData!: any[]  ;
  model: DataModel[] = [];
  readonly panelOpenState = signal(false);
  reportName = 'FX Blotter  from '
  constructor(
     public  dialog: MatDialog,
    private route: ActivatedRoute,
    private router: Router,
    private wsService: WebsocketService,
  ) {
    this.wsService.connect(API_URLS.WEBSOCKETS_TRADEFLOWS)
  }

  ngOnInit() {
    const today = new Date();
    this.reportName = this.reportName +
      `${formatDate(today, 'mediumDate', 'en-US')}` +
      ' To ' +
      `${formatDate(today, 'mediumDate', 'en-US')}`;

    this.model = [
      new DataModel('customer', 'Customer', 'Array', false, 'name', 'uppercase'),
      new DataModel('product', 'Product', 'Array', false, 'name', 'uppercase'),
      new DataModel('id', 'TradeId', 'string', false, [], 'uppercase'),
      new DataModel('val_date', 'ValDate', 'date', false, [],'date:shortDate'),
      new DataModel('tx_date', 'TxDate', 'date', false, [],'date:shortDate'),
      new DataModel('ccy1', 'Ccy1', 'Array', false, 'code', 'uppercase'),
      new DataModel('ccy2', 'Ccy2', 'Array', false, 'code', 'uppercase'),
      new DataModel('buy_sell', 'Buy/Sell', 'string', false, []),
      new DataModel('amount1', 'Ccy1_Amount', 'number', true, [],'`number:`1.2-2`'),
      new DataModel('amount2', 'Ccy2_Amount', 'number', false, [],'`number:`1.2-2`'),
      new DataModel('deal_rate', 'DealRate', 'number', false, [],'`number:`1.2-2`'),
      new DataModel('system_rate', 'ReevalRate', 'number', false, [],'`number:`1.2-2`'),
      new DataModel('fees_rate', 'Other Fees', 'number', false, [],'`number:`1.2-2`'),
      new DataModel('deal_pnl', 'PnL000', 'number', false, []),
      new DataModel('trader', 'Dealer', 'Array', false, 'name', 'uppercase'),
      new DataModel('status', 'Status', 'string', false, [],'uppercase'),
      new DataModel('last_updated', 'Last. Up', 'time', false, [],'date:`h:mm a`'),
    ];

    this.wsService.connect(API_URLS.WEBSOCKETS_TRADEFLOWS).subscribe( trade => {
      // console.log(trade.data);
      this.reportingData =[...trade.data]

    })

    // this.wsService.getMessages().subscribe( trade => {

    //   this.reportingData =[...trade.data]

    // })

  }

  tradeCapture() {
    let dialogConfig = new MatDialogConfig();
    // dialogConfig.disableClose = false;
    dialogConfig = {
      maxWidth: '800px',
      data: {
        currencies: this.route.snapshot.data['currencies'],
        products: this.route.snapshot.data['products'],
        customers: this.route.snapshot.data['customers'],
      },
    };
    //  dialogConfig.autoFocus = true;
    let dialogRef = this.dialog.open(TradeFormComponent, dialogConfig);

    dialogRef.afterClosed().subscribe((result: any) => {
      this.router.navigate(['.'], { relativeTo: this.route });
    });
  }

  ngOnDestroy(): void {
      this.wsService.disconnect()
  }


}
