import { TestBed } from '@angular/core/testing';

import { PositionUpdateService } from './position-update.service';

describe('PositionUpdateService', () => {
  let service: PositionUpdateService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PositionUpdateService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
