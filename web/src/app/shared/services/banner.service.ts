import { Injectable, Type } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class BannerService {
  private dynamicComponentSubject = new BehaviorSubject<Type<any> | null>(null);
  private bannerStateSubject = new BehaviorSubject<boolean>(false);
  bannerState$ = this.bannerStateSubject.asObservable();

  toggleBanner() {
    this.bannerStateSubject.next(!this.bannerStateSubject.value);
  }

  setDynamicComponent(componentType: Type<any>) {
    this.dynamicComponentSubject.next(componentType);
  }

  getDynamicComponent(): Observable<Type<any> | null> {
    return this.dynamicComponentSubject.asObservable();
  }
}
