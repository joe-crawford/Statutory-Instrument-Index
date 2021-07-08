import { ActivatedRoute } from '@angular/router';
import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTable } from '@angular/material/table';
import { StatutoryInstrumentsDataSource, StatutoryInstrument } from '../primary-acts/primary-acts-datasource';
import { Location } from '@angular/common';

@Component({
  selector: 'app-statutory-instruments',
  templateUrl: './statutory-instruments.component.html',
  styleUrls: ['./statutory-instruments.component.css']
})
export class StatutoryInstrumentsComponent implements AfterViewInit {
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;
  @ViewChild(MatTable) table!: MatTable<StatutoryInstrument>;
  dataSource: StatutoryInstrumentsDataSource;

  /** Columns displayed in the table. Columns IDs can be added, removed, or reordered. */
  displayedColumns = ['title', 'year', 'number', 'uri'];

  constructor(private route: ActivatedRoute, private location: Location) {
    this.dataSource = new StatutoryInstrumentsDataSource();
  }

  ngAfterViewInit(): void {
    this.dataSource.sort = this.sort;
    this.dataSource.paginator = this.paginator;
    this.dataSource.filter = {year: Number(this.route.snapshot.paramMap.get('year')), number: Number(this.route.snapshot.paramMap.get('number'))}
    this.table.dataSource = this.dataSource;
  }

  goBack(): void {
    this.location.back();
  }
}
