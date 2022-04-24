# -*- encoding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import _, api, fields, models


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    stage_progress = fields.Float('Progress (%)', required=True, default=10.0)

    _sql_constraints = [
        ('check_stage_progress', 'check(stage_progress >= 0 and stage_progress <= 100)', 'The Progress should be between 0% and 100%!')
    ]


class Task(models.Model):
    _inherit = "project.task"

    def _default_stage_progress(self):
        if 'default_stage_id' in self._context:
            stage_id = self._context.get('default_stage_id')
        else:
            stage_id = self._get_default_stage_id()
        if stage_id:
            return self.env['project.task.type'].browse(stage_id).stage_progress
        return 10

    stage_progress = fields.Float('Progress (%)', required=False, 
        default=lambda self: self._default_stage_progress(), tracking=True, group_operator="avg")

    _sql_constraints = [
        ('check_stage_progress', 'check(stage_progress >= 0 and stage_progress <= 100)', 'The Progress should be between 0% and 100%!')
    ]

    @api.model_create_multi
    def create(self, vals_list):
        tasks = super(Task, self).create(vals_list)
        for task in tasks:
            task.stage_progress = task.stage_id.stage_progress if task.stage_id else 10
        return tasks

    def write(self, vals):
        tasks = super(Task, self).write(vals)
        if vals.get('stage_id') and not vals.get('stage_progress'):
            task_task_type = self.env['project.task.type'].browse(vals['stage_id'])
            for task in self:
                task.stage_progress = task_task_type.stage_progress
        return tasks


class Project(models.Model):
    _inherit = "project.project"

    project_progress = fields.Float('Progress', store=True, compute="_compute_project_progress", group_operator="avg")

    @api.depends('task_ids', 'task_ids.stage_progress')
    def _compute_project_progress(self):
        for project in self:
            project.project_progress = round((sum(project.task_ids.mapped('stage_progress')) / len(project.task_ids.ids)), 2) if project.task_ids else 0.0


