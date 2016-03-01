# Creating images

* to make Harnaś GUI for setting up tests word, install [harnaś-tools](harnaś-tools.md).
* make sure that there are no locations other than `/tmp` and `/var/tmp` writable for user 10000, or user solutions could try to persist data between test runs. You can find them with find:

    ```
    sudo find / -perm -2 ! -type l -a ! -type c -a ! -type s -ls
    ```

    and fix these locations with `setfacl`.
