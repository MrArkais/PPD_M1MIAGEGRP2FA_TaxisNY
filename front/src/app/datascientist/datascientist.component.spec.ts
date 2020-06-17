import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DatascientistComponent } from './datascientist.component';

describe('DatascientistComponent', () => {
  let component: DatascientistComponent;
  let fixture: ComponentFixture<DatascientistComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DatascientistComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DatascientistComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
