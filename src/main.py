from exceptions.DAOException import DAOException

def main():
    try:
        raise DAOException("this is in the main function")
    except DAOException as message:
        print(message)
    except:
        print("caught something else")
    finally:
        print("in finally")

if __name__ == "__main__":
    main()