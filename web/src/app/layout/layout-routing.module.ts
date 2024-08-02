
import { LogoutComponent } from './logout/logout.component';
import { UserLoginComponent } from './user-login/user-login.component';
import { DashComponent } from './dash/dash.component';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PageNotFoundComponent } from '../shared/page-not-found/page-not-found.component';
import { TradesflowComponent } from '../treasuryapp/tradesflow/tradesflow.component';


const routes: Routes = [

  { path: '', component: DashComponent ,
  children: [
    { path: 'login', component: TradesflowComponent },
    { path: 'logout', component: LogoutComponent },
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
  exports: [RouterModule]
})
export class LayoutRoutingModule { }
