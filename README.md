# JFTTCompiler2018

Compiler prerequisites:
- python 3.6+
- pip3
- sly 0.3+

Installation of prerequisites:

```sh
$ sudo apt-get update
$ sudo apt-get install python3
$ sudo apt-get install python3-pip
$ pip3 install sly
```

To run compiler use:
```sh
$ python3 main.py <input> <output>
```

To run compiler in testing mode to compile all files in directory:
```sh
$ python3 main.py <test_dir> <outputs_dir> -test
```

To run assembly generated by compiler use script 'maszyna_rejestrowa' in 'maszyna_rejestrowa' directory.
```sh
$ ./maszyna_rejestrowa <assembly_code>
```

To run whole process of compilation, running assembly and testing against correct result use 'tester.py'
```sh
$ python3 tester.py
```
In script you can edit testing, output and result directory.

**Caution**

If script'maszyna_rejestrowa' does not work try recompiling it by using command.

``` sh
$ make
```
In 'maszyna_rejestrowa' directory.

