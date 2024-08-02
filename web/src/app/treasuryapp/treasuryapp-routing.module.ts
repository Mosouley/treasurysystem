
import { SegmentsResolver } from './../shared/resolvers/segments.resolver';
import { ProductsResolver } from './../shared/resolvers/products.resolver';
import { CurrenciesResolver } from './../shared/resolvers/currencies.resolver';
import { WalletsizingComponent } from './walletsizing/walletsizing.component';
import { FxflowsComponent } from './fxflows/fxflows.component';
import { FxblotterComponent } from './fxblotter/fxblotter.component';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashComponent } from '../layout/dash/dash.component';
import { PageNotFoundComponent } from '../shared/page-not-found/page-not-found.component';
import { DealersResolver } from '../shared/resolvers/dealers.resolver';
import { CustomerResolver } from '../shared/resolvers/customers.resolver';
import { SettingsComponent } from './config/settings/settings.component';
import { TradesflowComponent } from './tradesflow/tradesflow.component';
import { TradesResolver } from '../shared/resolvers/trades.resolver';
import { SalesByPeriodComponent } from './sales-by-period/sales-by-period.component';
import { DashboardComponent } from '../layout/dashboard/dashboard.component';
import { UserLoginComponent } from '../layout/user-login/user-login.component';
import { MatDialogRef } from '@angular/material/dialog';
import { DynamicModelComponent } from './config/dynamic-model/dynamic-model.component';
import { GenericComponent } from './config/generic/generic.component';
import { CustomerComponent } from '../shared/entities/customer/customer.component';

const routes: Routes = [

  { path: '', component: DashComponent ,
  children: [
    { path: 'dashboard', component: DashboardComponent },
     { path: 'fxflows', component: FxflowsComponent },
     { path: 'tradesflow',
     component: TradesflowComponent,
     resolve: {
      currencies: CurrenciesResolver,
      products: ProductsResolver,
      segments: SegmentsResolver,
      traders: DealersResolver,
      customers: CustomerResolver,

    }
  },
     { path: 'fxblotter',
     component: FxblotterComponent,
     resolve: {
      currencies: CurrenciesResolver,
      products: ProductsResolver,
      segments: SegmentsResolver,
      traders: DealersResolver,
      customers: CustomerResolver
    }
  },
     { path: 'walletsizing', component: WalletsizingComponent },

     { path: 'settings', component: SettingsComponent },
     { path: 'model-configuration', component: DynamicModelComponent },
     { path: 'entity-configuration', component: CustomerComponent },
     { path: 'sales-per-period',
     component: SalesByPeriodComponent,
    resolve: {
      trades: TradesResolver
    } },
     {path: 'not-found', component: PageNotFoundComponent}
  ]
},

{
  path: '',
  redirectTo: '/',
  pathMatch: 'full'
},
{
  path: '**',
  redirectTo: '/not-found',
  pathMatch: 'full'
}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
  providers: [
    CurrenciesResolver,
    ProductsResolver,
    CustomerResolver,
    SegmentsResolver,
    DealersResolver,
    DealersResolver,
    TradesResolver,
    {provide: MatDialogRef, useValue: {}}

  ]
})
export class TreasuryappRoutingModule { }
