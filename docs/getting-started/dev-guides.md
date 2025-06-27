# Developer's Guide


## Things to do if JSON schema for metadata changes.

* Update the markdown files for doc by running following command from the root of the repo.

    ```bash
    python docs/doc.py
    ```

* Also make update to python models by running bash-script `codegen.sh`.
* Refactor where updates classes are used through out the code base.