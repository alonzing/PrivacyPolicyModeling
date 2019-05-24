import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PpUrlSearchComponent } from './pp-url-search.component';

describe('PpUrlSearchComponent', () => {
  let component: PpUrlSearchComponent;
  let fixture: ComponentFixture<PpUrlSearchComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PpUrlSearchComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PpUrlSearchComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
