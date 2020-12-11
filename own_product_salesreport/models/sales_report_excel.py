import datetime
from odoo.exceptions import UserError
from datetime import datetime, date
import time
from odoo import api, models, _
from odoo.exceptions import UserError
from xlsxwriter.utility import xl_range, xl_rowcol_to_cell


class OwnproductXls(models.AbstractModel):
    _name = 'report.own_product_salesreport.action_own_product_xls'
    _inherit = 'report.report_xlsx.abstract'

    def get_sale(self, data):

        lines = []

        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        operating_unit = data['form']['operating_unit']
        target_move = data['form']['target_move']

        sl = 0
        if target_move==True:


            query = '''

              select to_char(date_trunc('day',s.date_order),'YYYY-MM-DD')::date as saledate,
                          pt.name as product_name,p.id as product_id,pt.list_price,sum(sl.product_uom_qty) as qty,
                          sum(sl.price_tax) as tax,sum(sl.price_total) as total_amount,sum(sl.price_subtotal) as untax_amount
                           from sale_order_line as sl
					left join sale_order as s on (sl.order_id=s.id)
					left join product_product as p on (sl.product_id=p.id)
					left join product_template as pt on (pt.id=p.product_tmpl_id)

					where
                        s.state in  ('sale') and pt.own_product=true
                        and  to_char(date_trunc('day',s.date_order),'YYYY-MM-DD')::date between %s and %s
                        and s.operating_unit_id= %s group by s.date_order,p.id,pt.id 
                        order by s.date_order
                       '''

            self.env.cr.execute(query, (
                date_from, date_to, operating_unit
            ))
            for row in self.env.cr.dictfetchall():
                sl += 1

                saledate = row['saledate'] if row['saledate'] else " "
                product_name = row['product_name'] if row['product_name'] else " "
                list_price = row['list_price'] if row['list_price'] else " "
                qty = row['qty'] if row['qty'] else " "

                untax_amount = row['untax_amount'] if row['untax_amount'] else " "
                tax = row['tax'] if row['tax'] else 0
                total_amount = row['total_amount'] if row['total_amount'] else 0
                sale_new_date = datetime.strptime(str(saledate), '%Y-%m-%d').date().strftime('%d-%m-%Y')

                res = {
                    'sl_no': sl,
                    'saledate': sale_new_date,
                    'product_name': product_name if product_name else " ",
                    'list_price': list_price if list_price else 0.0,
                    'qty': qty if qty else 0.0,
                    'untax_amount': untax_amount if untax_amount else 0.0,
                    'tax': tax if tax else 0.0,
                    'total_amount': total_amount if total_amount else 0.0

                }

                lines.append(res)
            if lines:
                return lines
            else:
                return []
        elif target_move == False:


            query = '''

                                                  select sum(sl.product_uom_qty) as qty,
                                              sum(sl.price_tax) as tax,
                                              sum(sl.price_total) as total_amount,
                                              sum(sl.price_subtotal) as untax_amount
                                               from sale_order_line as sl
                    					left join sale_order as s on (sl.order_id=s.id)
                    					left join product_product as p on (sl.product_id=p.id)
                    					left join product_template as pt on (pt.id=p.product_tmpl_id)

                    					where
                                            s.state in  ('sale') and pt.own_product=true
                                            and  to_char(date_trunc('day',s.date_order),'YYYY-MM-DD')::date between %s and %s
                                            and s.operating_unit_id= %s
                                                           '''

            self.env.cr.execute(query, (
                    date_from, date_to, operating_unit
                ))
            for row in self.env.cr.dictfetchall():
                sl += 1

                qty = row['qty'] if row['qty'] else " "

                untax_amount = row['untax_amount'] if row['untax_amount'] else " "
                tax = row['tax'] if row['tax'] else 0
                total_amount = row['total_amount'] if row['total_amount'] else 0

                res = {
                    'sl_no': sl,

                    'qty': qty if qty else 0.0,
                    'untax_amount': untax_amount if untax_amount else 0.0,
                    'tax': tax if tax else 0.0,
                    'total_amount': total_amount if total_amount else 0.0

                }

                lines.append(res)

            if lines:
                return lines
            else:
                return []

    def generate_xlsx_report(self, workbook, data, lines):

        if not data.get('form') or not self.env.context.get('active_model'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        sheet = workbook.add_worksheet(_('Own Product Sales Report'))
        sheet.set_landscape()
        sheet.set_default_row(25)
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(80)
        # sheet.set_column(0, 0, 14)
        # sheet.set_column(1, 1, 45)
        # sheet.set_column(2, 2, 22)
        # sheet.set_column(3, 5, 18)
        # sheet.set_column(4, 5, 20)


        # sheet.set_column(1, 1, 20)
        # sheet.set_column(2, 2, 25)
        # sheet.set_column(3, 3, 25)
        # sheet.set_column(4, 4, 20)
        # sheet.set_column(5, 5, 25)
        # sheet.set_column(6, 6, 20)
        # sheet.set_column(7, 7, 20)
        # sheet.set_column(8, 8, 20)
        # sheet.set_column(9, 9, 20)
        # sheet.set_column(10, 10, 20)
        # sheet.set_column(11, 11, 20)
        # sheet.set_column(12, 12, 20)
        # sheet.set_column(13, 13, 20)
        # sheet.set_column(14, 14, 20)
        # sheet.set_column(15, 15, 20)
        # sheet.set_column(16, 16, 20)
        # sheet.set_column(17, 17, 20)
        # sheet.set_column(18, 18, 20)
        # sheet.set_column(19, 19, 20)
        # sheet.set_column(20, 20, 20)
        # sheet.set_column(21, 21, 30)
        # sheet.set_column(22, 22, 20)
        # sheet.set_column(23, 23, 20)
        # sheet.set_column(24, 24, 20)

        company = self.env['res.company'].browse(data['form']['operating_unit'])

        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        operating_unit = data['form']['operating_unit']
        target_move = data['form']['target_move']
        if company.street:
            res = company.street
        else:
            res=""
        if company.street2:
            res2 = company.street2
        else:
            res2 = ""


        date_start = data['form']['date_from']
        date_end = data['form']['date_to']
        if date_start:

            date_object_date_start = datetime.strptime(date_start, '%Y-%m-%d').date()
        if date_end:
            date_object_date_end = datetime.strptime(date_end, '%Y-%m-%d').date()


        font_size_8 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 14})
        font_size_8_center = workbook.add_format(
            {'bottom': True, 'top': True, 'left': True, 'font_size': 14, 'align': 'center'})
        font_size_8_right = workbook.add_format(
            {'bottom': True, 'top': True, 'left': True, 'font_size': 14, 'align': 'right'})
        font_size_8_left = workbook.add_format(
            {'bottom': True, 'top': True, 'left': True, 'font_size': 14, 'align': 'left'})

        formattotal = workbook.add_format(
            {'bg_color': 'e2e8e8', 'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True,
             'align': 'right', 'bold': True})


        blue_mark2 = workbook.add_format(
            {'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 14, 'bold': True,
             'color': 'ffffff', 'bg_color': '7b0b5b', 'align': 'center'})
        font_size_8blod = workbook.add_format(
            {'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 14, 'bold': True, })

        blue_mark3 = workbook.add_format(
            {'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 18, 'bold': True,
             'color': 'ffffff', 'bg_color': '7b0b5b', 'align': 'center'})

        title_style = workbook.add_format({'font_size': 14, 'bold': True,
                                           'bg_color': '000000', 'color': 'ffffff',
                                           'bottom': 1, 'align': 'center'})
        account_style = workbook.add_format({'font_size': 14, 'bold': True,
                                           'bg_color': '929393', 'color': 'ffffff',
                                           'bottom': 1, 'align': 'left'})

        if target_move == True:

            sheet.set_column(1, 1, 20)
            sheet.set_column(2, 2, 25)
            sheet.set_column(3, 3, 25)
            sheet.set_column(4, 4, 20)
            sheet.set_column(5, 5, 25)
            sheet.set_column(6, 6, 20)
            sheet.set_column(7, 7, 20)
            sheet.set_column(8, 8, 20)
            sheet.set_column(9, 9, 20)
            sheet.set_column(10, 10, 20)
            sheet.set_column(11, 11, 20)
            sheet.set_column(12, 12, 20)
            sheet.set_column(13, 13, 20)
            sheet.set_column(14, 14, 20)
            sheet.set_column(15, 15, 20)
            sheet.set_column(16, 16, 20)
            sheet.set_column(17, 17, 20)
            sheet.set_column(18, 18, 20)
            sheet.set_column(19, 19, 20)
            sheet.set_column(20, 20, 20)
            sheet.set_column(21, 21, 30)
            sheet.set_column(22, 22, 20)
            sheet.set_column(23, 23, 20)
            sheet.set_column(24, 24, 20)

            sheet.merge_range('A1:H1', company.name, blue_mark3)
            sheet.merge_range('A2:H2', res+" ," + res2, blue_mark2)
            sheet.merge_range('A3:H3', " Own Product Sales Report", blue_mark2)

            self.model = self.env.context.get('active_model')
            docs = self.env[self.model].browse(self.env.context.get('active_ids', []))



            if date_start and date_end:

                sheet.merge_range('A5:H5', "Date : "+date_object_date_start.strftime('%d-%m-%Y')+ " to "+date_object_date_end.strftime('%d-%m-%Y'), font_size_8blod)
            elif date_start:
                sheet.merge_range('A5:H5', "Date : " + date_object_date_start.strftime('%d-%m-%Y') ,
                                  font_size_8blod)

            sheet.write('A6', "Sl No.", title_style)

            sheet.write('B6', "Date", title_style)
            sheet.write('C6', "Product", title_style)
            sheet.write('D6', "Unit Price", title_style)
            sheet.write('E6', "Qty", title_style)
            sheet.write('F6', "Tax Amount", title_style)
            sheet.write('G6', "Untax Amount", title_style)
            sheet.write('H6', "Total Amount", title_style)



            linw_row = 6
            line_column = 0


            for line in self.get_sale(data):
                sheet.write(linw_row, line_column, line['sl_no'], font_size_8_center)
                sheet.write(linw_row, line_column + 1, line['saledate'], font_size_8_left)

                sheet.write(linw_row, line_column + 2, line['product_name'], font_size_8_left)
                sheet.write(linw_row, line_column + 3, line['list_price'], font_size_8_center)
                sheet.write(linw_row, line_column + 4, '{0:,.2f}'.format(float(line['qty'])), font_size_8_center)
                sheet.write(linw_row, line_column + 5, '{0:,.2f}'.format(float(line['tax'])), font_size_8_center)

                sheet.write(linw_row, line_column + 6, '{0:,.2f}'.format(float(line['untax_amount'])), font_size_8_center)
                sheet.write(linw_row, line_column + 7, '{0:,.2f}'.format(float(line['total_amount'])), font_size_8_center)


                linw_row = linw_row + 1
                line_column = 0

            line_column = 0

            sheet.merge_range(linw_row, 0, linw_row, 3, "TOTAL", font_size_8_left)

            total_cell_range11 = xl_range(8, 5, linw_row - 1, 5)
            total_cell_range = xl_range(8, 4, linw_row - 1, 4)
            total_cell_range6 = xl_range(8, 6, linw_row - 1, 6)
            total_cell_range7 = xl_range(8, 7, linw_row - 1, 7)

            sheet.write_formula(linw_row, 5, '=SUM(' + total_cell_range11 + ')', font_size_8_center)
            sheet.write_formula(linw_row, 4, '=SUM(' + total_cell_range + ')', font_size_8_center)
            sheet.write_formula(linw_row, 6, '=SUM(' + total_cell_range6+ ')', font_size_8_center)
            sheet.write_formula(linw_row, 7, '=SUM(' + total_cell_range7 + ')', font_size_8_center)
        else:

            sheet.set_column(1, 1, 25)
            sheet.set_column(2, 2, 25)
            sheet.set_column(3, 3, 25)
            sheet.set_column(4, 4, 20)
            sheet.set_column(5, 5, 25)
            sheet.set_column(6, 6, 20)
            sheet.set_column(7, 7, 20)
            sheet.set_column(8, 8, 20)
            sheet.set_column(9, 9, 20)
            sheet.set_column(10, 10, 20)
            sheet.set_column(11, 11, 20)
            sheet.set_column(12, 12, 20)
            sheet.set_column(13, 13, 20)
            sheet.set_column(14, 14, 20)
            sheet.set_column(15, 15, 20)
            sheet.set_column(16, 16, 20)
            sheet.set_column(17, 17, 20)
            sheet.set_column(18, 18, 20)
            sheet.set_column(19, 19, 20)
            sheet.set_column(20, 20, 20)
            sheet.set_column(21, 21, 30)
            sheet.set_column(22, 22, 20)
            sheet.set_column(23, 23, 20)
            sheet.set_column(24, 24, 20)

            date_from = data['form']['date_from']
            date_to = data['form']['date_to']
            operating_unit = data['form']['operating_unit']
            target_move = data['form']['target_move']

            date_start = data['form']['date_from']
            date_end = data['form']['date_to']
            if date_start:
                date_object_date_start = datetime.strptime(date_start, '%Y-%m-%d').date()
            if date_end:
                date_object_date_end = datetime.strptime(date_end, '%Y-%m-%d').date()

            sheet.merge_range('A1:C1', company.name, blue_mark3)
            sheet.merge_range('A2:C2', res + " ," + res2, blue_mark2)
            # sheet.merge_range('A3:C3', " Own Product Sales Report", blue_mark2)
            # if date_start and date_end:
            #
            #     sheet.merge_range('A5:H5', "Date : " + date_object_date_start.strftime(
            #         '%d-%m-%Y') + " to " + date_object_date_end.strftime('%d-%m-%Y'), font_size_8blod)
            # elif date_start:
            #     sheet.merge_range('A5:H5', "Date : " + date_object_date_start.strftime('%d-%m-%Y'),
            #                       font_size_8blod)



            sheet.write('A4', "Report", font_size_8_left)

            sheet.merge_range('B4:C4', " Own Product Sales Report", font_size_8_left)
            # line_row = line_row + 1
            # line_column = 0

            sheet.write('A6', "Date", font_size_8_left)
            # line_row = line_row + 1
            # line_column = 1

            sheet.merge_range('B6:C6',date_object_date_start.strftime(
                    '%d-%m-%Y') + " to " + date_object_date_end.strftime('%d-%m-%Y'), font_size_8_left)
            # sheet.write(line_row, line_column, date_object_date_start.strftime(
            #         '%d-%m-%Y') + " to " + date_object_date_end.strftime('%d-%m-%Y'), font_size_8_left)
            # line_row = line_row + 1
            # line_column = 0

            sheet.write('A8', "Branch", font_size_8_left)
            # line_row = line_row + 1
            # line_column = 1
            sheet.merge_range('B8:C8', self.env['operating.unit'].browse(operating_unit).name, font_size_8_left)
            # line_row = line_row + 1
            # line_column = 0
            sheet.write('A10', "Qty", font_size_8_left)
            # line_row = line_row + 1
            # line_column = 1
            for line in self.get_sale(data):
                sheet.merge_range('B10:C10', '{0:,.2f}'.format(float(line['qty'])), font_size_8_left)
                # line_row = line_row + 1
                line_column = 0
            sheet.write('A12', "Tax Amount", font_size_8_left)
            # line_row = line_row + 1
            # line_column = 1
            for line in self.get_sale(data):
                sheet.merge_range('B12:C12', '{0:,.2f}'.format(float(line['tax'])), font_size_8_left)
                # line_row = line_row + 1
                line_column = 0
            sheet.write('A14', "Untax Amount", font_size_8_left)
            # line_row = line_row + 1
            # line_column = 1
            for line in self.get_sale(data):
                sheet.merge_range('B14:C14', '{0:,.2f}'.format(float(line['untax_amount'])), font_size_8_left)
                # line_row = line_row + 1
                line_column = 0

            sheet.write('A16', "Total Amount", font_size_8_left)
            # line_row = line_row + 1
            # line_column = 1
            for line in self.get_sale(data):
                sheet.merge_range('B16:C16', '{0:,.2f}'.format(float(line['total_amount'])), font_size_8_left)
                # line_row = line_row + 1
                line_column = 0







