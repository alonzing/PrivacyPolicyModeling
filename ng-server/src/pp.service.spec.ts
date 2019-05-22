import { TestBed } from '@angular/core/testing';

import { PpService } from './pp.service';

describe('PpService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: PpService = TestBed.get(PpService);
    expect(service).toBeTruthy();
  });
});
