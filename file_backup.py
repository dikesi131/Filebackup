from core import check_is_backuped
from core import logger
from core.get_parm import get_parameters
from core import get_config
from core import full_backup
from core import incremental_backup
from core import differential_backup
from core import send_message


def main():
    # init logger
    g_logger = logger.Logger()
    g_logger.pretreatment()
    conig = get_config.GetConfig()
    parser = get_parameters()
    args = parser.parse_args()
    dst_backup_path = args.output
    # get all level files
    all_files = conig.get_level_files_config()

    check = check_is_backuped.CheckIsBackup()
    f_backup = full_backup.FullBackup()
    incre_backup = incremental_backup.IncrementalBackup()
    diff_backup = differential_backup.DifferentialBackupFiles()
    send_email = send_message.SendEmail()
    if args.force:
        f_backup.full_file_backup(all_files, dst_backup_path)
    else:
        if check.is_backuped_path(dst_backup_path):
            incre_backup.incremental_backups_files(all_files, dst_backup_path)
            diff_backup.differential_backup_files(all_files, dst_backup_path)
        else:
            f_backup.full_file_backup(all_files, dst_backup_path)

    # send qq email
    send_email.send_qq_mail()


if __name__ == '__main__':
    main()
