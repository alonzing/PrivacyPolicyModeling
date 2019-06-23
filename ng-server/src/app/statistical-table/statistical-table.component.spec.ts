import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {StatisticalTableComponent} from './statistical-table.component';

describe('StatisticalTableComponent', () => {
  let component: StatisticalTableComponent;
  let fixture: ComponentFixture<StatisticalTableComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [StatisticalTableComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StatisticalTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
