"""Commands for the HuaWeiVBSClient"""


from osc_lib.command import command
import utils


class BackupCreate(command.Command):
    """Create a VBS backup."""

    def get_parser(self, prog_name):
        parser = super(BackupCreate, self).get_parser(prog_name)
        parser.add_argument('--volume-id',
                            required=True,
                            type=utils.check_id,
                            help='VBS volume ID which to create backup')
        parser.add_argument('--name',
                            required=True,
                            type=utils.check_name,
                            help='VBS Backup name to create')
        parser.add_argument('--description',
                            type=utils.check_description,
                            help='VBS Backup description to create')
        return parser

    def take_action(self, parsed_args):
        result = self.app.client_manager.huaweivbs.backup_create(
            parsed_args.volume_id,
            parsed_args.name,
            parsed_args.description)
        return 'Backup creating. Job ID is ' + result['job_id']


class BackupDelete(command.Command):
    """Delete a VBS backup."""

    def get_parser(self, prog_name):
        parser = super(BackupDelete, self).get_parser(prog_name)
        parser.add_argument('--backup-id',
                            required=True,
                            type=utils.check_id,
                            help='VBS Backup id which to be deleted')
        return parser

    def take_action(self, parsed_args):
        result = self.app.client_manager.huaweivbs.backup_delete(
            parsed_args.backup_id)
        return 'Backup deleting. Job ID is ' + result['job_id']


class BackupRestore(command.Command):
    """Restore a disk using a VBS backup"""

    def get_parser(self, prog_name):
        parser = super(BackupRestore, self).get_parser(prog_name)
        parser.add_argument('--backup-id',
                            required=True,
                            type=utils.check_id,
                            help='Backup ID to use with')
        parser.add_argument('--volume-id',
                            required=True,
                            type=utils.check_id,
                            help='Volume ID to restore')
        return parser

    def take_action(self, parsed_args):
        result = self.app.client_manager.huaweivbs.backup_restore(
            parsed_args.backup_id,
            parsed_args.volume_id)
        return 'Backup Restoring. Job ID is ' + result['job_id']


class BackupQueryStatus(command.ShowOne):
    """Show a job status."""

    def get_parser(self, prog_name):
        parser = super(BackupQueryStatus, self).get_parser(prog_name)
        parser.add_argument('--job-id',
                            required=True,
                            type=utils.check_id,
                            help='Backup job ID to query')
        return parser

    def take_action(self, parsed_args):
        result = self.app.client_manager.huaweivbs.backup_query_status(
            parsed_args.job_id)
        return utils.format_job_status(result)


class BackupList(command.Lister):
    """List backups."""

    def take_action(self, parsed_args):
        backups = self.app.client_manager.huaweivbs.backup_list()
        rows = ((i['name'], i['id']) for i in backups['backups'])
        return ('name', 'id'), rows
