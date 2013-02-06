#!/bin/bash

if [ -d municonv_dev_packages ]
then
	rm -rf municonv_dev_packages
fi

mkdir municonv_dev_packages

current_dir=`pwd`
if [[ "$current_dir" != *library* ]]
then
  echo "This command should be run from inside the library directory."
  exit
fi


package_dir="$current_dir/municonv_dev_packages"
source_dir="$current_dir/source"
echo "Installing packages into $package_dir"

#Keep django in the path
export PYTHONPATH=$package_dir/lib/python2.7/site-packages:$package_dir/lib/python2.6/site-packages:$package_dir/lib64/python2.7/site-packages:$package_dir/lib64/python2.6/site-packages
pip install $source_dir/Django-1.3.1.tar.gz --install-option="--prefix=$package_dir"
pip install $source_dir/MySQL-python-1.2.3.tar.gz --install-option="--prefix=$package_dir"
pip install $source_dir/django-extra-views-0.2.5.tar.gz --install-option="--prefix=$package_dir"
pip install $source_dir/django-crispy-forms-1.2.0.tar.gz --install-option="--prefix=$package_dir"
pip install $source_dir/nose-1.2.1.tar.gz --install-option="--prefix=$package_dir"
pip install $source_dir/django-nose-1.1.tar.gz --install-option="--prefix=$package_dir"
pip install $source_dir/wsgiref-0.1.2.zip --install-option="--prefix=$package_dir"
pip install $source_dir/nose-cov-1.6.tar.gz --install-option="--prefix=$package_dir"
