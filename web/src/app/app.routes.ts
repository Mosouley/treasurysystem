import { Routes } from '@angular/router';

export const routes: Routes = [

  { path: 'home', loadChildren: () => import('./layout/layout.module').then(m => m.LayoutModule) },
  { path: '', loadChildren: () => import('./treasuryapp/treasuryapp.module').then(m => m.TreasuryappModule) },
  {
    path: '',
    redirectTo: '/home',
    pathMatch: 'full'
  },
  {
    path: '**',
    redirectTo: '/home',
    pathMatch: 'full'
  }

];
