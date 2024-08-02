import { ReactiveFormsModule } from '@angular/forms';
import { TreasuryappRoutingModule } from './treasuryapp-routing.module';
import { NgModule } from '@angular/core';
import { CommonModule, CurrencyPipe, DecimalPipe } from '@angular/common';
import { FxblotterComponent } from './fxblotter/fxblotter.component';
import { MaterialModule } from '../material/material.module';
import { SharedModule } from '../shared/shared.module';
import { FxflowsComponent } from './fxflows/fxflows.component';
import { WalletsizingComponent } from './walletsizing/walletsizing.component';
import { TradeComponent } from './fxblotter/trade.component';
import { DataTableComponent } from './config/data-table/data-table.component';
import { ImportFileComponent } from './config/import-file.component';
import { TradesflowComponent } from './tradesflow/tradesflow.component';
import { TradeService } from '../shared/services/trade.service';
import { WebsocketService } from '../shared/services/websocket.service';



@NgModule({
    imports: [
        CommonModule,
        ReactiveFormsModule,
        TreasuryappRoutingModule,
        MaterialModule,
        SharedModule,
        FxblotterComponent,
        FxflowsComponent,
        WalletsizingComponent,
        TradeComponent,
        DataTableComponent,
        ImportFileComponent,
        TradesflowComponent,
    ],
    providers: [DecimalPipe, CurrencyPipe, TradeService, WebsocketService]
})
export class TreasuryappModule { }
