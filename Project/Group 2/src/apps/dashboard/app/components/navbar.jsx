export default function Navbar(){
    return (
      <>
        <nav className="bg-white border-gray-200">
          <div className="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl p-4">
            <a
              href="https://flowbite.com"
              className="flex items-center space-x-3 rtl:space-x-reverse"
            >
              <p className="text-4xl animate-bounce">
                🏃‍♀️
              </p>
              <span className="self-center text-2xl font-semibold whitespace-nowrap">
                Dashboard 
              </span>
            </a>

          </div>
        </nav>

      </>
    );
}