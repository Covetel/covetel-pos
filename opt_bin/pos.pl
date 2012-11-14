#!/usr/bin/perl 
use Proc::Daemon; 
use common::sense;

my $arg = shift || die "Usage: {start|stop|status}";

sub start;
sub stop;
sub status;
my $daemon;

$daemon->{'display'} = {
    name          =>  'Display',
    work_dir      =>  '/opt/covetel/pos',
    child_STDOUT  =>  'log/display.log',
    child_STDERR  =>  '+>>log/error_display.log',
    pid_file      =>  'run/display.pid',
    exec_command  =>  ['python /opt/covetel/pos/bin/display.py'], 
};

$daemon->{'print'} = {
    name          =>  'Print',
    work_dir      =>  '/opt/covetel/pos',
    child_STDOUT  =>  'log/print.log',
    child_STDERR  =>  '+>>log/error_print.log',
    pid_file      =>  'run/print.pid',
    exec_command  =>  ['python /opt/covetel/pos/bin/print-server.py'], 
};

given ($arg) {
  when (/start/) {
          foreach (keys %{$daemon}){
            my $pid = start $daemon->{$_} unless status $daemon->{$_};
            printf "Starting [%s]\n", $daemon->{$_}->{'name'} if $pid;
          }
  }
  when (/stop/){
          foreach (keys %{$daemon}){
            my $pid = stop $daemon->{$_};
            printf "Stoping [%s]\n", $daemon->{$_}->{'name'} if $pid;
          }
  }
  when (/status/){
          foreach (keys %{$daemon}){
            my $pid = status $daemon->{$_};
            if ($pid){
              printf "[%s]: running with pid: %d\n", $daemon->{$_}->{'name'}, $pid;
            } else {
              printf "[%s]: is not running\n", $daemon->{$_}->{'name'};
            }
          }

  }
  when (/restart/){
  }

}


sub start {
  my $daemon = shift; 
  my $d = Proc::Daemon->new(
    work_dir      =>  $daemon->{'work_dir'},
    child_STDOUT  =>  $daemon->{'child_STDOUT'},
    child_STDERR  =>  $daemon->{'child_STDERR'},
    pid_file      =>  $daemon->{'pid_file'},
    exec_command  =>  $daemon->{'exec_command'},
  );
  my $pid = $d->Init;
  return $pid;
}

sub status {
  my $daemon = shift; 
  my $pid_file = $daemon->{'work_dir'} .'/'. $daemon->{'pid_file'};
  my $d = Proc::Daemon->new( 
    work_dir => $daemon->{'work_dir'},
  );
  return $d->Status($pid_file);
}

sub stop {
  my $daemon = shift; 
  my $pid_file = $daemon->{'work_dir'} .'/'. $daemon->{'pid_file'};
  my $d = Proc::Daemon->new( 
    work_dir => $daemon->{'work_dir'},
  );
  my $pid = $d->Kill_Daemon($pid_file);
  return $pid; 
}
