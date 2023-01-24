#! /bin/bash

#colors
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

echo "${red}Welcome to dett....${reset}"
echo "${green}What do you want ?..."
printf "1) clear => for clearing all migrations related file
2) initial => for initial setup
3) mig => for migration and migrate
4) app app_name=> create app with given name
5) su -> create superuser
6) te => Basic Exception handling generator
7) url => URLS Generator
input a choice: ${reset} "

#script section for re executing the task
re_work(){
    echo "${red}Select a choice${reset}"
    printf "1) clear => for clearing all migrations related file
  2) initial => for initial setup
  3) mig => for migration and migrate
  4) app app_name=> create app with given name
  5) su -> create superuser
  6) te => Basic Exception handling generator
  7) url => URLS Generator
   input a choice: ${reset} "
  check_config
}

check_config(){
  read -r what
  if [ "$what" == "initial" ];
  then

    echo "Script Executing Started...."

    echo "Running Migrations..."
    python manage.py makemigrations
    echo "Migrations completed"

    echo "Starting Migrate...."
    python manage.py migrate
    echo "Migrated !!"

    echo "Starting Load data...."
    python manage.py loaddata initial_data permissions user_groups permissions user_groups extras notification phone
    echo "Loaddata finished...."
    echo "Lets re run server "
    echo "Lets Rock !!!"
    re_work
fi

  if [ "$what" == "clear" ];
  then
    echo "Clearing all migrations pyc and py files......."
    find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
    find . -path "*/migrations/*.pyc"  -delete
    echo "Cleared all migrations files.."
    echo "Do migrations and migrate alsooo....."
    re_work
  fi

  if [ "$what" == "mig" ];
  then
    echo "Performing Migrations..."
    python manage.py makemigrations
    echo "Migrations completed !"

    echo "Performing Migrate Operation..."
    python manage.py migrate
    echo "Migrate operation completed..!"
    re_work
  fi

  if [ "$what" == "su" ];
  then
    echo "Creating Super user ..."
    python manage.py createsuperuser
    echo "ending Super user programme.."
    re_work
  fi

  if [ "$what" == "te" ];
  then
    echo "
    response_data = {}
    try:
      pass
    except Exception as e:
      pass
    else:
      pass
    "
    re_work
  fi
}
check_config