#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging, datetime
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from zup.models import Job


logger = logging.getLogger('zup.clean')


# usage type:
#  
# python manage.py clean
# 
class Command(BaseCommand):
  
  args = ''
  help = 'execute some job on corpus.'
  option_list = BaseCommand.option_list

  def handle(self, *args, **options):
    logger.info('doing some cleaning')
    
    now = timezone.now()

    for job in Job.objects.all():
      try:
        if (now - job.date_last_modified).days > 2: # more than two days ago
          logger.info('removing job "%s" because of its obsolesence of %s days' % (job.name, (now - job.date_last_modified).days))
          job.delete()
      except Exception, e:
        logger.info('problem during cleaning ...')
        logger.exception(e)

    logger.info('cleaning complete')