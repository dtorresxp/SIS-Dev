from datetime import datetime
from odoo import models, fields, api
import random


class Student(models.Model):

    # _inherit = 'sis_student'

    @api.depends('name', 'surname')
    def _make_unique(self):
        r = random.randint(1, 101)
        unique = self.name+self.surname+str(r)
        print(unique)
        return unique

    _name = 'sis.student'
    _description = 'student model'

    name = fields.Char(string='Name',
                       required=True)
    surname = fields.Char(string='Surname', required=True)

    state = fields.Boolean(string='Accepted', default=False)
    unique = fields.Char(compute=_make_unique, readonly=True)

    dob = fields.Date('Date of Birth')

    id = fields.Integer(string='ID')
    password = fields.Char(string='Password', required=True)

    programme = fields.Many2one('sis.programme', string='Programme Name')

    current_year = fields.Integer(string='Current Year', required=True, default=1, readonly=True)
    transcript = fields.Binary(string='Transcript')

    address = fields.Char(string='Address')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email', required=True)

    highest_qualification = fields.Selection([
        ('matric', 'Matric Certificate'),
        ('bachelors', 'Bachelors')
    ])

    school = fields.Char(string='School')

    userid = fields.Char(string='User ID', readonly=True)

    courses = fields.Many2many('sis.courses',string='All taken courses')

    @api.model
    def create(self, vals):
        # Create the user
        res = super(Student, self).create(vals)
        self.env['res.users'].create({
            'name':vals['name'],
            'email':vals['email'],
            'login':vals['email'],
            'new_password':vals['password']
        })


    @api.multi
    def accept(self):
        # self.user_id
        # Create the Student
        # res = super(Student, self).create(vals)

        # MAKE USER
        res = self.env['res.users'].create({'name': self.name,
                                            'email': self.email,
                                            'login': self.email,
                                            'new_password': self.password})

        self.userid = res.id

        print(self.programme.courses[0].department.department)
        for i in range(0, len(self.programme.courses)):
            student_course = self.programme.courses[i].name
            course_department = self.programme.courses[i].department
            print("---->", student_course, "*", course_department)

        # Assign the group
        student_group = self.env.ref('sis.student_group')
        res.groups_id = student_group
