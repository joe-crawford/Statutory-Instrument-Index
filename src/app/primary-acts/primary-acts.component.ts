import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTable } from '@angular/material/table';
import { PrimaryActsDataSource, PrimaryAct } from './primary-acts-datasource';

@Component({
  selector: 'app-primary-acts',
  templateUrl: './primary-acts.component.html',
  styleUrls: ['./primary-acts.component.css']
})
export class PrimaryActsComponent implements AfterViewInit {
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;
  @ViewChild(MatTable) table!: MatTable<PrimaryAct>;
  dataSource: PrimaryActsDataSource;
  filterValue = "";

  /** Columns displayed in the table. Columns IDs can be added, removed, or reordered. */
  displayedColumns = ['title', 'year', 'number', 'count', 'uri'];

  constructor() {
    this.dataSource = new PrimaryActsDataSource();
  }

  ngAfterViewInit(): void {
    this.dataSource.sort = this.sort;
    this.dataSource.paginator = this.paginator;
    this.table.dataSource = this.dataSource;
  }
}
