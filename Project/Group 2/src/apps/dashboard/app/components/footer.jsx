export default function Footer() {
  return (
    <>
      <footer className="bg-white rounded-lg shadow m-4">
        <div className="w-full mx-auto max-w-screen-xl p-4 md:flex md:items-center md:justify-between">
          <span className="text-sm text-gray-500 sm:text-center">
            © 2024{" "}
            <a href="https://flowbite.com/" className="hover:underline">
              ส่วนหนึ่งของงาน
            </a>
             Hardware
          </span>
          <ul className="flex flex-wrap items-center mt-3 text-sm font-medium text-gray-500 sm:mt-0">
            <li>
              <a href="https://github.com/karitthorn/hardware-dashboard" className="hover:underline me-4 md:me-6">
                Github
              </a>
            </li>
          </ul>
        </div>
      </footer>
    </>
  );
}
